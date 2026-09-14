import SwiftUI

struct HomeView: View {
    @EnvironmentObject var authManager: AuthManager

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                Text("PlumiHope")
                    .font(.largeTitle)
                    .fontWeight(.bold)

                if let user = authManager.currentUser {
                    Text("Welcome, \(user.fullName)")
                        .font(.headline)
                }

                Text("Find a cause you can confidently support.")
                    .foregroundColor(.secondary)

                Spacer()

                Button("Sign out", role: .destructive) {
                    authManager.logout()
                }
            }
            .padding()
        }
    }
}

#Preview {
    HomeView()
        .environmentObject(AuthManager.shared)
}
