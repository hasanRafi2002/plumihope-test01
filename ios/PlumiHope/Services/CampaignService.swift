import Foundation

struct PaginatedCampaigns: Codable {
    let items: [Campaign]
    let page: Int
    let pageSize: Int
    let total: Int
    let hasNext: Bool

    enum CodingKeys: String, CodingKey {
        case items
        case page
        case pageSize = "page_size"
        case total
        case hasNext = "has_next"
    }
}

struct WhyVerified: Codable {
    let agentIdentityReviewed: Bool
    let caseInvestigated: Bool
    let evidenceReviewed: Bool
    let campaignModeratorApproved: Bool
    let lastReviewedAt: Date?
    let disclaimer: String

    enum CodingKeys: String, CodingKey {
        case agentIdentityReviewed = "agent_identity_reviewed"
        case caseInvestigated = "case_investigated"
        case evidenceReviewed = "evidence_reviewed"
        case campaignModeratorApproved = "campaign_moderator_approved"
        case lastReviewedAt = "last_reviewed_at"
        case disclaimer
    }
}

final class CampaignService {
    static let shared = CampaignService()
    private let client = APIClient.shared

    private init() {}

    func discover(query: String? = nil, page: Int = 1) async throws -> PaginatedCampaigns {
        var items: [URLQueryItem] = [URLQueryItem(name: "page", value: String(page))]
        if let query = query, !query.isEmpty {
            items.append(URLQueryItem(name: "q", value: query))
        }
        let endpoint = APIEndpoint(path: "/campaigns/discover", method: .get, requiresAuth: false, queryItems: items)
        return try await client.request(endpoint)
    }

    func getCampaign(id: UUID) async throws -> Campaign {
        let endpoint = APIEndpoint(path: "/campaigns/\(id.uuidString)", method: .get, requiresAuth: false)
        return try await client.request(endpoint)
    }

    func getWhyVerified(campaignId: UUID) async throws -> WhyVerified {
        let endpoint = APIEndpoint(path: "/campaigns/\(campaignId.uuidString)/why-verified", method: .get, requiresAuth: false)
        return try await client.request(endpoint)
    }
}
