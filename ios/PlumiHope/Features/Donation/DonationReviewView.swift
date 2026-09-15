import SwiftUI

struct DonationReviewView: View {
    @StateObject private var viewModel: DonationReviewViewModel
    @Environment(\.dismiss) private var dismiss

    init(campaign: Campaign, amount: Double) {
        _viewModel = StateObject(wrappedValue: DonationReviewViewModel(campaign: campaign, amount: amount))
    }

    var body: some View {
        Group {
            if viewModel.isConfirmed, let donation = viewModel.donation {
                DonationConfirmedView(donation: donation) {
                    dismiss()
                }
            } else if viewModel.paymentInitiated {
                DonationPendingView()
            } else if viewModel.isLoading && viewModel.donation == nil {
                ProgressView("Preparing your donation...")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if let errorMessage = viewModel.errorMessage {
                VStack(spacing: 12) {
                    Text(errorMessage)
                        .foregroundColor(.secondary)
                    Button("Try again") {
                        Task { await viewModel.createDonation() }
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if let donation = viewModel.donation {
                VStack(spacing: 20) {
                    Text("Your donation")
                        .font(.headline)
                        .frame(maxWidth: .infinity, alignment: .leading)

                    VStack(spacing: 12) {
                        feeRow("Campaign contribution", donation.feeBreakdown.donationAmount)
                        feeRow("Payment fee", donation.feeBreakdown.paymentFee)
                        feeRow("Platform fee", donation.feeBreakdown.platformFee)
                        Divider()
                        feeRow("Net amount", donation.feeBreakdown.netAmount, emphasized: true)
                        Divider()
                        feeRow("Total charged", donation.feeBreakdown.totalCharged, emphasized: true)
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)

                    Spacer()

                    Button {
                        Task { await viewModel.proceedToPayment() }
                    } label: {
                        if viewModel.isLoading {
                            ProgressView().frame(maxWidth: .infinity)
                        } else {
                            Text("Continue to payment").frame(maxWidth: .infinity)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(viewModel.isLoading)
                }
                .padding()
            } else {
                // SAFETY NET — if you see this, none of the states above matched.
                // This should never happen; if it does, the printed state below
                // tells us exactly what combination is unhandled.
                VStack(spacing: 12) {
                    Text("Unexpected state")
                        .font(.headline)
                    Text(debugStateDescription)
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .padding(.horizontal)
                    Button("Retry") {
                        Task { await viewModel.createDonation() }
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .onAppear {
                    print("DEBUG: SAFETY NET HIT — \(debugStateDescription)")
                }
            }
        }
        .navigationTitle(viewModel.isConfirmed ? "" : "Review")
        .navigationBarTitleDisplayMode(.inline)
        .navigationBarBackButtonHidden(viewModel.isConfirmed)
        .task {
            print("DEBUG: DonationReviewView .task fired — donation is nil? \(viewModel.donation == nil)")
            if viewModel.donation == nil {
                await viewModel.createDonation()
            }
        }
    }

    /// Plain Swift String built first, then handed to Text(_:) as-is.
    /// Avoids the "appendedInterpolation is deprecated" warning that comes
    /// from interpolating non-localizable types (Bool, etc.) directly
    /// inside a Text("...") literal, which builds a LocalizedStringKey.
    private var debugStateDescription: String {
        let isConfirmedStr = String(viewModel.isConfirmed)
        let paymentInitiatedStr = String(viewModel.paymentInitiated)
        let isLoadingStr = String(viewModel.isLoading)
        let hasDonationStr = String(viewModel.donation != nil)
        let errorStr = viewModel.errorMessage ?? "nil"
        return "isConfirmed=\(isConfirmedStr), paymentInitiated=\(paymentInitiatedStr), isLoading=\(isLoadingStr), donation=\(hasDonationStr), error=\(errorStr)"
    }

    private func feeRow(_ label: String, _ value: String, emphasized: Bool = false) -> some View {
        HStack {
            Text(label)
                .foregroundColor(emphasized ? .primary : .secondary)
                .fontWeight(emphasized ? .semibold : .regular)
            Spacer()
            Text("৳\(value)")
                .fontWeight(emphasized ? .semibold : .regular)
        }
    }
}

struct DonationPendingView: View {
    var body: some View {
        VStack(spacing: 16) {
            ProgressView()
            Text("Donation processing")
                .font(.headline)
            Text("Your payment is being verified. We'll confirm the donation once the payment provider confirms the transaction.")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
