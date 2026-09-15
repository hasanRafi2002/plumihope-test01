import Foundation

extension Notification.Name {
    /// Posted when the refresh token itself is invalid/expired and the user
    /// must be sent back to the login screen. AuthManager listens for this.
    static let sessionExpired = Notification.Name("com.plumihope.sessionExpired")
}

/// Serializes concurrent refresh attempts so that if multiple requests hit
/// a 401 at nearly the same time, only one actual /auth/refresh call is made
/// and all callers share its result.
private actor RefreshCoordinator {
    private var inFlightTask: Task<Bool, Never>?

    func refreshIfNeeded(_ operation: @escaping () async -> Bool) async -> Bool {
        if let task = inFlightTask {
            return await task.value
        }
        let task = Task { await operation() }
        inFlightTask = task
        let result = await task.value
        inFlightTask = nil
        return result
    }
}

final class APIClient {
    static let shared = APIClient()

    private let baseURL = "http://localhost:8000/api/v1"
    private let tokenStore: TokenStore = KeychainTokenStore()
    private let refreshCoordinator = RefreshCoordinator()
    private let decoder: JSONDecoder = {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return decoder
    }()
    private let encoder: JSONEncoder = {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        return encoder
    }()

    private init() {}

    func request<T: Decodable>(
        _ endpoint: APIEndpoint,
        body: Encodable? = nil
    ) async throws -> T {
        let data = try await requestData(endpoint, body: body)
        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            throw APIError.decodingFailed(error)
        }
    }

    func requestNoContent(_ endpoint: APIEndpoint, body: Encodable? = nil) async throws {
        _ = try await requestData(endpoint, body: body)
    }

    private func requestData(_ endpoint: APIEndpoint, body: Encodable?, isRetry: Bool = false) async throws -> Data {
        guard var components = URLComponents(string: baseURL + endpoint.path) else {
            throw APIError.invalidURL
        }
        components.queryItems = endpoint.queryItems

        guard let url = components.url else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        if endpoint.requiresAuth, let token = tokenStore.getAccessToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        if let body = body {
            request.httpBody = try encoder.encode(body)
        }

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.unknown(URLError(.badServerResponse))
        }

        switch httpResponse.statusCode {
        case 200...299:
            return data
        case 401:
            // Only attempt a refresh for authenticated endpoints, and only once
            // per original request (isRetry guards against a refresh loop if the
            // freshly-refreshed token somehow also comes back 401).
            if endpoint.requiresAuth && !isRetry {
                let refreshed = await refreshCoordinator.refreshIfNeeded { [weak self] in
                    await self?.performRefresh() ?? false
                }
                if refreshed {
                    return try await requestData(endpoint, body: body, isRetry: true)
                }
            }
            tokenStore.clearTokens()
            NotificationCenter.default.post(name: .sessionExpired, object: nil)
            throw APIError.unauthorized
        case 403:
            throw APIError.forbidden
        case 404:
            throw APIError.notFound
        default:
            let message = (try? decoder.decode([String: String].self, from: data))?["detail"] ?? "Server error"
            throw APIError.serverError(statusCode: httpResponse.statusCode, message: message)
        }
    }

    /// Attempts to exchange the stored refresh token for a new access/refresh
    /// token pair. Returns false (without throwing) on any failure — an
    /// expired/revoked refresh token, a network error, or a malformed
    /// response all just mean "refresh didn't work," which the caller
    /// handles by forcing logout.
    private func performRefresh() async -> Bool {
        guard let refreshToken = tokenStore.getRefreshToken() else {
            print("DEBUG: token refresh skipped — no refresh token stored")
            return false
        }
        guard let url = URL(string: baseURL + "/auth/refresh") else { return false }

        struct RefreshRequestBody: Encodable {
            let refreshToken: String
            enum CodingKeys: String, CodingKey { case refreshToken = "refresh_token" }
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        do {
            request.httpBody = try encoder.encode(RefreshRequestBody(refreshToken: refreshToken))
            let (data, response) = try await URLSession.shared.data(for: request)

            guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
                print("DEBUG: token refresh rejected by server")
                return false
            }

            let tokens = try decoder.decode(TokenResponse.self, from: data)
            tokenStore.saveTokens(accessToken: tokens.accessToken, refreshToken: tokens.refreshToken)
            print("DEBUG: access token refreshed silently")
            return true
        } catch {
            print("DEBUG: token refresh failed: \(error)")
            return false
        }
    }
}
