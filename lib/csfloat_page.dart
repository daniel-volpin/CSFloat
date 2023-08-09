import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'csfloat_http_service.dart';
import 'csfloat_trade_data.dart';

class PostsPage extends StatelessWidget {
  final HttpService httpService = HttpService();

  PostsPage({Key? key}) : super(key: key);

  Widget buildCsfloatCard(CSFloat csfloatData) {
    return Card(
      elevation: 2,
      child: ListTile(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Listing ID: ${csfloatData.itemID}"),
            const SizedBox(height: 4),
            Text("Item price: ${csfloatData.price}"),
            const SizedBox(height: 4),
            Text("Item Information: ${csfloatData.itemInfo.marketHashName}"),
            if (csfloatData.sellerInfo!.steamID != null) ...[
              const SizedBox(height: 4),
              Text("Seller Steam ID: ${csfloatData.sellerInfo!.steamID}"),
            ],
            if (csfloatData.itemInfo.inspectLink != null &&
                csfloatData.itemInfo.inspectLink is String &&
                csfloatData.itemInfo.inspectLink.isNotEmpty) ...[
              const SizedBox(height: 4),
              buildInspectionLink(csfloatData.itemInfo.inspectLink),
            ],
          ],
        ),
      ),
    );
  }

  Widget buildInspectionLink(String inspectLink) {
    return RichText(
      text: TextSpan(
        children: [
          const TextSpan(text: "Inspection URL: "),
          TextSpan(
            text: inspectLink,
            style: const TextStyle(
              color: Colors.blue,
              decoration: TextDecoration.underline,
            ),
            recognizer: TapGestureRecognizer()
              ..onTap = () {
                launchUrl(Uri.parse(inspectLink));
              },
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("CSFloat Listed Items"),
      ),
      body: FutureBuilder<List<CSFloat>>(
        future: httpService.getPosts(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const CircularProgressIndicator();
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          } else if (snapshot.hasData) {
            final csfloatData = snapshot.data!;
            return ListView(
              children: csfloatData.map<Widget>((CSFloat csfloat) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
                  child: buildCsfloatCard(csfloat),
                );
              }).toList(),
            );
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}
