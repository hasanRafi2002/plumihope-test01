import Foundation

struct AppNotification: Codable, Identifiable {
    let id: UUID
    let notificationType: String
    let title: String
    let body: String?
    let readAt: Date?
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id
        case notificationType = "notification_type"
        case title
        case body
        case readAt = "read_at"
        case createdAt = "created_at"
    }
}
