import SwiftUI

struct DonationConfirmedView: View {
    let donation: DonationDetail
    var onDone: () -> Void = {}

    var body: some View {
        VStack(spacing: 20) {
            Spacer()

            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 64))
                .foregroundColor(.green)

            Text("Donation confirmed")
                .font(.title2)
                .fontWeight(.bold)

            Text("৳\(donation.amount)")
                .font(.largeTitle)
                .fontWeight(.semibold)

            Text("Your donation has been verified.")
                .font(.subheadline)
                .foregroundColor(.secondary)

            Spacer()

            NavigationLink {
                DonationReceiptView(donation: donation)
            } label: {
                Text("View receipt")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)

            Button("Done") {
                onDone()
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 8)
        }
        .padding()
    }
}
