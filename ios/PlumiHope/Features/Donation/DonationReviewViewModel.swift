import Foundation
import Combine

@MainActor
final class DonationReviewViewModel: ObservableObject {
    @Published var donation: DonationDetail?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var paymentInitiated: Bool = false

    private let donationService = DonationService.shared
    let campaign: Campaign
    let amount: Double

    init(campaign: Campaign, amount: Double) {
        self.campaign = campaign
        self.amount = amount
    }

    func createDonation() async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        do {
            donation = try await donationService.createDonation(campaignId: campaign.id, amount: amount)
            print("DEBUG: donation created successfully: \(String(describing: donation))")
        } catch {
            print("DEBUG: createDonation failed: \(error)")
            errorMessage = error.localizedDescription
        }
    }

    func proceedToPayment() async {
        guard let donation = donation else { return }
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        do {
            let result = try await donationService.initiatePayment(donationId: donation.id)
            print("DEBUG: payment initiated: \(result)")
            paymentInitiated = true
        } catch {
            print("DEBUG: proceedToPayment failed: \(error)")
            errorMessage = error.localizedDescription
        }
    }
}
