import Foundation

struct User: Codable, Identifiable {
    let id: UUID
    let fullName: String
    let email: String
    let phone: String?
    let status: String

    enum CodingKeys: String, CodingKey {
        case id
        case fullName = "full_name"
        case email
        case phone
        case status
    }
}
