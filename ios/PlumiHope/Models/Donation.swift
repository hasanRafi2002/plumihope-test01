import Foundation

struct Donation: Codable, Identifiable {
    let id: UUID
    let campaignId: UUID
    let amount: String
    let currency: String
    let status: String
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id
        case campaignId = "campaign_id"
        case amount
        case currency
        case status
        case createdAt = "created_at"
    }

    var amountValue: Double { Double(amount) ?? 0 }
}
