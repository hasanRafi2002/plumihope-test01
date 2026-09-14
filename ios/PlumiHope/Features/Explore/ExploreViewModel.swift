import Foundation
import Combine

@MainActor
final class ExploreViewModel: ObservableObject {
    @Published var campaigns: [Campaign] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var searchText: String = ""

    private let campaignService = CampaignService.shared

    func loadCampaigns() async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        do {
            let result = try await campaignService.discover(query: searchText.isEmpty ? nil : searchText)
            campaigns = result.items
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
