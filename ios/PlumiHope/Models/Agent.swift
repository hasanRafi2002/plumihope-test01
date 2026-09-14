import Foundation

struct AgentProfile: Codable, Identifiable {
    let id: UUID
    let userId: UUID
    let status: String
    let fullName: String
    let location: String?
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case status
        case fullName = "full_name"
        case location
        case createdAt = "created_at"
    }
}
