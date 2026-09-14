import SwiftUI

struct ExploreView: View {
    @StateObject private var viewModel = ExploreViewModel()
    @State private var selectedCampaignId: UUID?

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.isLoading && viewModel.campaigns.isEmpty {
                    ProgressView()
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else if let errorMessage = viewModel.errorMessage {
                    VStack(spacing: 12) {
                        Text("Couldn't load campaigns")
                            .font(.headline)
                        Text(errorMessage)
                            .font(.footnote)
                            .foregroundColor(.secondary)
                        Button("Try again") {
                            Task { await viewModel.loadCampaigns() }
                        }
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else if viewModel.campaigns.isEmpty {
                    VStack(spacing: 12) {
                        Text("No campaigns found")
                            .font(.headline)
                        Text("Try another search term.")
                            .font(.footnote)
                            .foregroundColor(.secondary)
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    ScrollView {
                        LazyVStack(spacing: 16) {
                            ForEach(viewModel.campaigns) { campaign in
                                Button {
                                    selectedCampaignId = campaign.id
                                } label: {
                                    CampaignCard(campaign: campaign)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding()
                    }
                }
            }
            .navigationTitle("Discover")
            .searchable(text: $viewModel.searchText, prompt: "Search campaigns...")
            .onSubmit(of: .search) {
                Task { await viewModel.loadCampaigns() }
            }
            .navigationDestination(item: $selectedCampaignId) { campaignId in
                CampaignDetailView(campaignId: campaignId)
            }
            .task {
                await viewModel.loadCampaigns()
            }
        }
    }
}

#Preview {
    ExploreView()
}
