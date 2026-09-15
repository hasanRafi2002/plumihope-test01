import Foundation
import Combine

@MainActor
final class AuthManager: ObservableObject {
    static let shared = AuthManager()

    @Published var isAuthenticated: Bool = false
    @Published var currentUser: User?
    @Published var sessionExpiredMessage: String?

    private let tokenStore: TokenStore = KeychainTokenStore()
    private var cancellables = Set<AnyCancellable>()

    private init() {
        isAuthenticated = tokenStore.getAccessToken() != nil

        NotificationCenter.default.publisher(for: .sessionExpired)
            .receive(on: DispatchQueue.main)
            .sink { [weak self] _ in
                self?.handleSessionExpired()
            }
            .store(in: &cancellables)
    }

    func saveSession(accessToken: String, refreshToken: String) {
        tokenStore.saveTokens(accessToken: accessToken, refreshToken: refreshToken)
        isAuthenticated = true
        sessionExpiredMessage = nil
    }

    func logout() {
        tokenStore.clearTokens()
        isAuthenticated = false
        currentUser = nil
        sessionExpiredMessage = nil
    }

    func setCurrentUser(_ user: User) {
        currentUser = user
    }

    /// Called when APIClient determines the refresh token itself is no
    /// longer valid (expired, revoked, or missing). Distinct from a manual
    /// logout() so the login screen can explain why the user landed there.
    private func handleSessionExpired() {
        guard isAuthenticated else { return }
        tokenStore.clearTokens()
        isAuthenticated = false
        currentUser = nil
        sessionExpiredMessage = "Your session has expired. Please sign in again."
    }
}
