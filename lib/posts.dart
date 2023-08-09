import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'http_service.dart';
import 'post_model.dart';

class PostsPage extends StatelessWidget {
  final HttpService httpService = HttpService();

  PostsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("CSFloat Listed Items"),
      ),
      body: FutureBuilder(
        future: httpService.getPosts(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const CircularProgressIndicator();
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          } else if (snapshot.hasData) {
            final csfloatData = snapshot.data!;
            return ListView(
              children: csfloatData.map<Widget>(
                (CSFloat csfloatData) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
                    child: Card(
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
                            if (csfloatData.sellerInfo!.steamID != null)
                              const SizedBox(height: 4),
                              Text("Seller Steam ID: ${csfloatData.sellerInfo!.steamID}"),
                            if (csfloatData.itemInfo.inspectLink != null && csfloatData.itemInfo.inspectLink is String && csfloatData.itemInfo.inspectLink.isNotEmpty)
                              const SizedBox(height: 4),
                              RichText(
                                text: TextSpan(
                                  children: [
                                    const TextSpan(text: "Inspection URL: "),
                                    TextSpan(
                                      text: csfloatData.itemInfo.inspectLink,
                                      style: const TextStyle(
                                        color: Colors.blue,
                                        decoration: TextDecoration.underline,
                                      ),
                                      recognizer: TapGestureRecognizer()
                                        ..onTap = () {
                                          launchUrl(Uri.parse(csfloatData.itemInfo.inspectLink));
                                        },
                                    ),
                                  ],
                                ),
                              ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              ).toList(),
            );
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}