import Foundation

struct TokenResponse: Codable {
    let accessToken: String
    let refreshToken: String
    let tokenType: String

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case tokenType = "token_type"
    }
}

struct RegisterRequest: Encodable {
    let fullName: String
    let email: String
    let password: String

    enum CodingKeys: String, CodingKey {
        case fullName = "full_name"
        case email
        case password
    }
}

struct LoginRequest: Encodable {
    let email: String
    let password: String
}

final class AuthService {
    static let shared = AuthService()
    private let client = APIClient.shared

    private init() {}

    func register(fullName: String, email: String, password: String) async throws -> TokenResponse {
        let body = RegisterRequest(fullName: fullName, email: email, password: password)
        let endpoint = APIEndpoint(path: "/auth/register", method: .post, requiresAuth: false)
        return try await client.request(endpoint, body: body)
    }

    func login(email: String, password: String) async throws -> TokenResponse {
        let body = LoginRequest(email: email, password: password)
        let endpoint = APIEndpoint(path: "/auth/login", method: .post, requiresAuth: false)
        return try await client.request(endpoint, body: body)
    }

    func getCurrentUser() async throws -> User {
        let endpoint = APIEndpoint(path: "/auth/me", method: .get, requiresAuth: true)
        return try await client.request(endpoint)
    }
}
