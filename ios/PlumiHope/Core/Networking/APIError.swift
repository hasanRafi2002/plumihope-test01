import Foundation

enum APIError: Error, LocalizedError {
    case invalidURL
    case noData
    case decodingFailed(Error)
    case serverError(statusCode: Int, message: String)
    case unauthorized
    case forbidden
    case notFound
    case unknown(Error)

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL."
        case .noData:
            return "No data received from server."
        case .decodingFailed:
            return "Failed to decode server response."
        case .serverError(_, let message):
            return message
        case .unauthorized:
            return "Your session has expired. Please sign in again."
        case .forbidden:
            return "You don't have permission to perform this action."
        case .notFound:
            return "The requested resource was not found."
        case .unknown(let error):
            return error.localizedDescription
        }
    }
}
