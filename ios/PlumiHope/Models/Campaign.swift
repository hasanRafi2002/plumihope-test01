import Foundation

struct Campaign: Codable, Identifiable {
    let id: UUID
    let title: String
    let description: String
    let categoryId: UUID
    let targetAmount: String
    let raisedAmount: String
    let currency: String
    let status: String
    let verificationStatus: String
    let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id
        case title
        case description
        case categoryId = "category_id"
        case targetAmount = "target_amount"
        case raisedAmount = "raised_amount"
        case currency
        case status
        case verificationStatus = "verification_status"
        case createdAt = "created_at"
    }

    var targetAmountValue: Double { Double(targetAmount) ?? 0 }
    var raisedAmountValue: Double { Double(raisedAmount) ?? 0 }
    var progressPercent: Double {
        guard targetAmountValue > 0 else { return 0 }
        return min(raisedAmountValue / targetAmountValue, 1.0)
    }
}
