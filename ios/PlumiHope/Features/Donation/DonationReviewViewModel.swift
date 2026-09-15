import Foundation
import Combine

@MainActor
final class DonationReviewViewModel: ObservableObject {
    @Published var donation: DonationDetail?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var paymentInitiated: Bool = false
    @Published var isConfirmed: Bool = false

    private let donationService = DonationService.shared
    let campaign: Campaign
    let amount: Double

    init(campaign: Campaign, amount: Double) {
        self.campaign = campaign
        self.amount = amount
        print("DEBUG: DonationReviewViewModel init — campaign=\(campaign.id) amount=\(amount)")
    }

    func createDonation() async {
        print("DEBUG: createDonation() ENTERED")
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        do {
            donation = try await donationService.createDonation(campaignId: campaign.id, amount: amount)
            print("DEBUG: createDonation SUCCESS — status=\(donation?.status ?? "nil")")
        } catch {
            print("DEBUG: createDonation FAILED: \(error)")
            errorMessage = error.localizedDescription
        }
        print("DEBUG: createDonation() EXIT — isLoading=\(isLoading), donation=\(donation != nil), errorMessage=\(errorMessage ?? "nil")")
    }

    func proceedToPayment() async {
        print("DEBUG: proceedToPayment() ENTERED")
        guard let donation = donation else {
            print("DEBUG: proceedToPayment() aborted — donation is nil")
            return
        }
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }

        do {
            let result = try await donationService.initiatePayment(donationId: donation.id)
            print("DEBUG: payment initiated: \(result)")
            paymentInitiated = true

            // DEV/SANDBOX ONLY — see DonationService.simulateSandboxWebhook.
            try await donationService.simulateSandboxWebhook(providerReference: result.providerReference)
            print("DEBUG: sandbox webhook simulated")

            try await pollForConfirmation(donationId: donation.id)
        } catch {
            print("DEBUG: proceedToPayment FAILED: \(error)")
            errorMessage = error.localizedDescription
            paymentInitiated = false
        }
    }

    private func pollForConfirmation(donationId: UUID) async throws {
        for attempt in 1...5 {
            let updated = try await donationService.getDonation(id: donationId)
            print("DEBUG: poll attempt \(attempt) — status: \(updated.status)")
            self.donation = updated
            if updated.status == "CONFIRMED" {
                isConfirmed = true
                return
            }
            try await Task.sleep(nanoseconds: 500_000_000)
        }
        errorMessage = "Your donation is still being verified. Please check back in a moment."
        paymentInitiated = false
    }
}
