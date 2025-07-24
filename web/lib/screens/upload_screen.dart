import 'dart:html';
import 'package:flutter/material.dart';
import 'package:ai_insights/ai_service.dart';
import 'package:ai_insights/screens/preview_screen.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({super.key});

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  List<List<dynamic>>? previewData;
  String? fileId;
  bool isLoading = false;

  void pickFileAndUpload() async {
    print('[UploadScreen] File picker triggered...');
    FileUploadInputElement uploadInput = FileUploadInputElement()..accept = '.csv,.xlsx';
    uploadInput.click();

    uploadInput.onChange.listen((event) async {
      final file = uploadInput.files!.first;
      print('[UploadScreen] File selected: ${file.name}, size: ${file.size} bytes');
      setState(() => isLoading = true);

      try {
        final result = await ApiService.uploadFile(file);
        debugPrint('[UploadScreen] Upload result: $result');

        final previewRaw = result['preview'];
        if (previewRaw is List) {
          previewData = List<List<dynamic>>.from(previewRaw);
        } else if (previewRaw is Map) {
          previewData = previewRaw.values.map((row) => List<dynamic>.from(row)).toList();
        } else {
          previewData = null;
        }


        setState(() {
          previewData = previewData;
          fileId = result['file_id'];
          isLoading = false;
        });

        print('[UploadScreen] Preview data loaded. File ID: $fileId');
      } catch (e) {
        print('[UploadScreen] Upload failed: $e');
        setState(() => isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Upload failed: $e')),
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    print('[UploadScreen] build() called — isLoading: $isLoading, fileId: $fileId');

    return Scaffold(
      appBar: AppBar(title: const Text('Upload Data File')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ElevatedButton.icon(
              onPressed: isLoading ? null : pickFileAndUpload,
              icon: const Icon(Icons.upload_file),
              label: isLoading
                  ? const Text('Uploading...')
                  : const Text('Upload CSV or Excel File'),
            ),
            const SizedBox(height: 20),
            if (previewData != null) ...[
              const Text('Preview (First 5 Rows):',
                  style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              Expanded(
                child: ListView.builder(
                  itemCount: previewData!.length,
                  itemBuilder: (context, index) {
                    final row = previewData![index];
                    print('[UploadScreen] Preview row [$index]: $row');
                    return Text(row.join(' | '));
                  },
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (fileId != null) {
                    print('[UploadScreen] Navigating to PreviewScreen with fileId: $fileId');
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PreviewScreen(fileId: fileId!),
                      ),
                    );
                  } else {
                    print('[UploadScreen] fileId is null, not navigating');
                  }
                },
                child: const Text('Generate Insights'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

