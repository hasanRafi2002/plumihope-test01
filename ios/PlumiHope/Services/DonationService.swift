import Foundation

struct FeeBreakdown: Codable {
    let donationAmount: String
    let paymentFee: String
    let platformFee: String
    let netAmount: String
    let totalCharged: String
    let policyVersion: String

    enum CodingKeys: String, CodingKey {
        case donationAmount = "donation_amount"
        case paymentFee = "payment_fee"
        case platformFee = "platform_fee"
        case netAmount = "net_amount"
        case totalCharged = "total_charged"
        case policyVersion = "policy_version"
    }
}

struct DonationDetail: Codable {
    let id: UUID
    let campaignId: UUID
    let amount: String
    let currency: String
    let status: String
    let createdAt: Date
    let feeBreakdown: FeeBreakdown

    enum CodingKeys: String, CodingKey {
        case id
        case campaignId = "campaign_id"
        case amount
        case currency
        case status
        case createdAt = "created_at"
        case feeBreakdown = "fee_breakdown"
    }
}

struct DonationCreateRequest: Encodable {
    let campaignId: UUID
    let amount: Double

    enum CodingKeys: String, CodingKey {
        case campaignId = "campaign_id"
        case amount
    }
}

struct PaymentInitiateRequest: Encodable {
    let donationId: UUID

    enum CodingKeys: String, CodingKey {
        case donationId = "donation_id"
    }
}

struct PaymentInitiateResponse: Codable {
    let paymentId: UUID
    let provider: String
    let providerReference: String
    let redirectUrl: String
    let status: String

    enum CodingKeys: String, CodingKey {
        case paymentId = "payment_id"
        case provider
        case providerReference = "provider_reference"
        case redirectUrl = "redirect_url"
        case status
    }
}

private struct WebhookRequest: Encodable {
    let providerReference: String

    enum CodingKeys: String, CodingKey {
        case providerReference = "provider_reference"
    }
}

final class DonationService {
    static let shared = DonationService()
    private let client = APIClient.shared

    private init() {}

    func createDonation(campaignId: UUID, amount: Double) async throws -> DonationDetail {
        let body = DonationCreateRequest(campaignId: campaignId, amount: amount)
        let endpoint = APIEndpoint(path: "/donations", method: .post, requiresAuth: true)
        return try await client.request(endpoint, body: body)
    }

    func initiatePayment(donationId: UUID) async throws -> PaymentInitiateResponse {
        let body = PaymentInitiateRequest(donationId: donationId)
        let endpoint = APIEndpoint(path: "/payments/initiate", method: .post, requiresAuth: true)
        return try await client.request(endpoint, body: body)
    }

    func getDonation(id: UUID) async throws -> DonationDetail {
        let endpoint = APIEndpoint(path: "/donations/\(id.uuidString)", method: .get, requiresAuth: true)
        return try await client.request(endpoint)
    }

    func listMyDonations() async throws -> [Donation] {
        let endpoint = APIEndpoint(path: "/donations/me", method: .get, requiresAuth: true)
        return try await client.request(endpoint)
    }

    /// DEV/SANDBOX ONLY: there is no real payment gateway calling back to our
    /// webhook in local development, so the client simulates that server-to-server
    /// callback itself after "completing" a sandbox payment. This must never be
    /// called against a real provider — real providers call the webhook themselves.
    func simulateSandboxWebhook(providerReference: String) async throws {
        let body = WebhookRequest(providerReference: providerReference)
        let endpoint = APIEndpoint(path: "/payments/webhooks/sandbox", method: .post, requiresAuth: false)
        try await client.requestNoContent(endpoint, body: body)
    }
}
