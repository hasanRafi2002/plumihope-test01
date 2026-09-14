import Foundation
import Combine

@MainActor
final class CampaignDetailViewModel: ObservableObject {
    @Published var campaign: Campaign?
    @Published var whyVerified: WhyVerified?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?

    private let campaignService = CampaignService.shared
    let campaignId: UUID

    init(campaignId: UUID) {
        self.campaignId = campaignId
    }

    func load() async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        do {
            async let campaignResult = campaignService.getCampaign(id: campaignId)
            async let whyVerifiedResult = campaignService.getWhyVerified(campaignId: campaignId)

            campaign = try await campaignResult
            whyVerified = try await whyVerifiedResult
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
