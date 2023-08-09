import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'csfloat_http_service.dart';
import 'csfloat_trade_data.dart';

class PostsPage extends StatelessWidget {
  final HttpService httpService = HttpService();

  PostsPage({Key? key}) : super(key: key);

  Widget buildCSFloatCard(CSFloat csfloatData) {
    return Card(
      elevation: 2,
      child: Container(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SelectableText("Listing ID: ${csfloatData.itemID}"),
            const SizedBox(height: 4),
            SelectableText("Seller Steam ID: ${csfloatData.sellerInfo!.steamID}"),
            const SizedBox(height: 4),
            SelectableText("Item Name: ${csfloatData.itemInfo.marketHashName}"),
            const SizedBox(height: 4),
            Text("Item price: ${csfloatData.price}"),
            const SizedBox(height: 4),
            Container(
              child: buildInspectionLink(csfloatData.itemInfo.inspectLink),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildInspectionLink(String inspectLink) {
    return GestureDetector(
      onTap: () {
        launchUrl(Uri.parse(inspectLink));
      },
      child: const Text(
        "Inspect Item",
        style: TextStyle(
          color: Colors.blue,
          decoration: TextDecoration.underline,
        ),
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
            return GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 4,
              ),
              itemCount: csfloatData.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: buildCSFloatCard(csfloatData[index]),
                );
              },
            );
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}
