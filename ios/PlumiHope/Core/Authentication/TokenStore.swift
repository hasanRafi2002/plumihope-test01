protocol TokenStore {
    func saveTokens(accessToken: String, refreshToken: String)
    func getAccessToken() -> String?
    func getRefreshToken() -> String?
    func clearTokens()
}
