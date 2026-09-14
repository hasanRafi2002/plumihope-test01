import SwiftUI

struct CampaignDetailView: View {
    @StateObject private var viewModel: CampaignDetailViewModel

    init(campaignId: UUID) {
        _viewModel = StateObject(wrappedValue: CampaignDetailViewModel(campaignId: campaignId))
    }

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView()
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if let errorMessage = viewModel.errorMessage {
                Text(errorMessage)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if let campaign = viewModel.campaign {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        RoundedRectangle(cornerRadius: 16)
                            .fill(Color(.systemGray5))
                            .frame(height: 200)

                        Text("✓ VERIFIED CASE")
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(.green)

                        Text(campaign.title)
                            .font(.title2)
                            .fontWeight(.bold)

                        VStack(alignment: .leading, spacing: 8) {
                            Text("\(formattedAmount(campaign.raisedAmountValue)) raised")
                                .font(.title3)
                                .fontWeight(.semibold)
                            Text("of \(formattedAmount(campaign.targetAmountValue))")
                                .foregroundColor(.secondary)

                            ProgressView(value: campaign.progressPercent)
                                .tint(.green)
                        }

                        NavigationLink {
                            DonationAmountView(campaign: campaign)
                        } label: {
                            Text("Donate")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.borderedProminent)

                        Text("ABOUT")
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(.secondary)
                        Text(campaign.description)

                        if let whyVerified = viewModel.whyVerified {
                            WhyVerifiedSection(whyVerified: whyVerified)
                        }
                    }
                    .padding()
                }
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .task {
            await viewModel.load()
        }
    }

    private func formattedAmount(_ value: Double) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.maximumFractionDigits = 0
        formatter.groupingSeparator = ","
        return "৳" + (formatter.string(from: NSNumber(value: value)) ?? "0")
    }
}

struct WhyVerifiedSection: View {
    let whyVerified: WhyVerified

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("WHY VERIFIED?")
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(.secondary)

            checkRow("Agent identity reviewed", whyVerified.agentIdentityReviewed)
            checkRow("Case investigated", whyVerified.caseInvestigated)
            checkRow("Evidence reviewed", whyVerified.evidenceReviewed)
            checkRow("Campaign reviewed by Moderator", whyVerified.campaignModeratorApproved)

            Text(whyVerified.disclaimer)
                .font(.caption2)
                .foregroundColor(.secondary)
                .padding(.top, 4)
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }

    private func checkRow(_ label: String, _ checked: Bool) -> some View {
        HStack {
            Image(systemName: checked ? "checkmark.circle.fill" : "circle")
                .foregroundColor(checked ? .green : .secondary)
            Text(label)
                .font(.subheadline)
        }
    }
}
