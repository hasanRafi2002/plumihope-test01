import SwiftUI

struct DonationReviewView: View {
    @StateObject private var viewModel: DonationReviewViewModel

    init(campaign: Campaign, amount: Double) {
        _viewModel = StateObject(wrappedValue: DonationReviewViewModel(campaign: campaign, amount: amount))
    }

    var body: some View {
        Group {
            if viewModel.paymentInitiated {
                DonationPendingView()
            } else if viewModel.isLoading && viewModel.donation == nil {
                ProgressView()
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
            }
        }
        .navigationTitle("Review")
        .navigationBarTitleDisplayMode(.inline)
        .task {
            if viewModel.donation == nil {
                await viewModel.createDonation()
            }
        }
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
