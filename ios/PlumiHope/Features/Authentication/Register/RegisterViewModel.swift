import Foundation
import Combine

@MainActor
final class RegisterViewModel: ObservableObject {
    @Published var fullName: String = ""
    @Published var email: String = ""
    @Published var password: String = ""
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?

    private let authService = AuthService.shared
    private let authManager = AuthManager.shared

    func register() async {
        errorMessage = nil
        isLoading = true
        defer { isLoading = false }

        do {
            let tokens = try await authService.register(fullName: fullName, email: email, password: password)
            authManager.saveSession(accessToken: tokens.accessToken, refreshToken: tokens.refreshToken)

            let user = try await authService.getCurrentUser()
            authManager.setCurrentUser(user)
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
