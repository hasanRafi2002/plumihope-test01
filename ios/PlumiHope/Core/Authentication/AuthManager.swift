import Foundation
import Combine

@MainActor
final class AuthManager: ObservableObject {
    static let shared = AuthManager()

    @Published var isAuthenticated: Bool = false
    @Published var currentUser: User?

    private let tokenStore: TokenStore = KeychainTokenStore()

    private init() {
        isAuthenticated = tokenStore.getAccessToken() != nil
    }

    func saveSession(accessToken: String, refreshToken: String) {
        tokenStore.saveTokens(accessToken: accessToken, refreshToken: refreshToken)
        isAuthenticated = true
    }

    func logout() {
        tokenStore.clearTokens()
        isAuthenticated = false
        currentUser = nil
    }

    func setCurrentUser(_ user: User) {
        currentUser = user
    }
}
