import Foundation

struct Report: Codable, Identifiable {
    let id: UUID
    let entityType: String
    let entityId: UUID
    let reason: String
    let status: String
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id
        case entityType = "entity_type"
        case entityId = "entity_id"
        case reason
        case status
        case createdAt = "created_at"
    }
}
