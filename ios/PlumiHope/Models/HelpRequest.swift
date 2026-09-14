import Foundation

struct HelpRequest: Codable, Identifiable {
    let id: UUID
    let userId: UUID
    let category: String
    let subcategory: String?
    let description: String
    let location: String?
    let status: String
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case category
        case subcategory
        case description
        case location
        case status
        case createdAt = "created_at"
    }
}
