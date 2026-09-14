import Foundation

struct APIEndpoint {
    let path: String
    let method: HTTPMethod
    let requiresAuth: Bool
    let queryItems: [URLQueryItem]?

    init(path: String, method: HTTPMethod = .get, requiresAuth: Bool = true, queryItems: [URLQueryItem]? = nil) {
        self.path = path
        self.method = method
        self.requiresAuth = requiresAuth
        self.queryItems = queryItems
    }
}
