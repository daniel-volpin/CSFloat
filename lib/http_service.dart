import 'dart:convert';
import 'post_model.dart';
import 'package:http/http.dart' as http;

class HttpService {
  Future<List<CSFloat>> getPosts() async {
    var url = Uri.https('csfloat.com', '/api/v1/listings');

    Map<String, String> requestHeaders = {
      'Authorization': '42d6X7eI1wZo7mCXETV4_a-HzzAtkpsB'
    };

    try {
      var response = await http.get(url, headers: requestHeaders);

      if (response.statusCode == 200) {
        List<dynamic> body = jsonDecode(response.body);

        List<CSFloat> posts = body
          .map(
            (dynamic item) => CSFloat.fromJson(item),
          )
          .where((csFloat) =>
              csFloat.sellerInfo?.steamID != null &&
              csFloat.sellerInfo?.steamID.isNotEmpty &&
              !csFloat.itemInfo.marketHashName.toLowerCase().contains('sticker')) // Filter out items with "Sticker" in marketHashName
          .toList();

        return posts;
      } else {
        print("Error: ${response.statusCode}");
        return [];
      }
    } catch (error) {
      print("Error: $error");
      return [];
    }
  }
}