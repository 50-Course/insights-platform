import 'dart:async';
import 'dart:convert';
import 'dart:html';
import 'dart:typed_data';
import 'package:flutter/foundation.dart'; // for debugPrint
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';

  static Future<Map<String, dynamic>> uploadFile(File file) async {
    debugPrint('[ApiService] Preparing to upload file: ${file.name}');

    final reader = FileReader();
    final completer = Completer<Uint8List>();

    reader.readAsArrayBuffer(file);
    reader.onLoadEnd.listen((event) {
      completer.complete(reader.result as Uint8List);
    });

    final bytes = await completer.future;
    debugPrint('[ApiService] File read into memory, size: ${bytes.length} bytes');

    final request = http.MultipartRequest('POST', Uri.parse('$baseUrl/upload'));
    request.files.add(http.MultipartFile.fromBytes(
      'file',
      bytes,
      filename: file.name,
    ));

    try {
      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      debugPrint('[ApiService] Upload response status: ${response.statusCode}');
      debugPrint('[ApiService] Upload response body: $responseBody');

      return jsonDecode(responseBody);
    } catch (e) {
      debugPrint('[ApiService] Upload failed with error: $e');
      rethrow;
    }
  }

  static Future<List<dynamic>> processInsights(String fileId) async {
    final uri = Uri.parse('$baseUrl/process');
    debugPrint('[ApiService] Sending process request for fileId: $fileId to $uri');

    try {
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'file_id': fileId}),
      );

      debugPrint('[ApiService] Process response status: ${response.statusCode}');
      debugPrint('[ApiService] Process response body: ${response.body}');

    // we want to check for succecessful response codes, we return 201 on the backend, but well ideally that was menat to be 200
      if (response.statusCode == 200 || response.statusCode == 201) {
        return jsonDecode(response.body)['insights'];
      } else {
        throw Exception('Failed to process insights (Status: ${response.statusCode})');
      }
    } catch (e) {
      debugPrint('[ApiService] Error during processInsights: $e');
      rethrow;
    }
  }

  static Future<List<dynamic>> fetchInsightsByFileId(String fileId) async {
    final uri = Uri.parse('$baseUrl/insights?file_id=$fileId');
    debugPrint('[ApiService] Fetching insights for fileId: $fileId from $uri');

    try {
      final response = await http.get(uri);

      debugPrint('[ApiService] Fetch response status: ${response.statusCode}');
      debugPrint('[ApiService] Fetch response body: ${response.body}');

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to fetch insights (Status: ${response.statusCode})');
      }
    } catch (e) {
      debugPrint('[ApiService] Error during fetchInsightsByFileId: $e');
      rethrow;
    }
  }
}

