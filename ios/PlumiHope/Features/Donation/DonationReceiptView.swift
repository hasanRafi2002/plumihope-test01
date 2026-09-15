import SwiftUI

struct DonationReceiptView: View {
    let donation: DonationDetail

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Donation receipt")
                .font(.title2)
                .fontWeight(.bold)

            receiptRow("Donation ID", donation.id.uuidString)
            receiptRow("Amount", "৳\(donation.amount)")
            receiptRow("Status", donation.status)
            receiptRow("Date", donation.createdAt.formatted(date: .abbreviated, time: .shortened))

            Spacer()
        }
        .padding()
        .navigationTitle("Receipt")
        .navigationBarTitleDisplayMode(.inline)
    }

    private func receiptRow(_ label: String, _ value: String) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(label)
                .font(.caption)
                .foregroundColor(.secondary)
            Text(value)
                .font(.body)
        }
    }
}
