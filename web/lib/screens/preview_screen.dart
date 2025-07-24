import 'package:flutter/material.dart';
import 'package:ai_insights/ai_service.dart';


class PreviewScreen extends StatefulWidget {
  final String fileId;

  const PreviewScreen({super.key, required this.fileId});

  @override
  State<PreviewScreen> createState() => _PreviewScreenState();
}

class _PreviewScreenState extends State<PreviewScreen> {
  List<dynamic>? insights;
  bool isLoading = false;
  String? errorMessage;

  void fetchInsights() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final result = await ApiService.processInsights(widget.fileId);
      setState(() {
        insights = result;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        errorMessage = 'Failed to generate insights: $e';
        isLoading = false;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    fetchInsights();
  }

  Widget _buildInsightCard(Map<String, dynamic> insight) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      elevation: 3,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(insight['title'] ?? 'Untitled Insight',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                )),
            const SizedBox(height: 8),
            Text(insight['description'] ?? '',
                style: const TextStyle(fontSize: 14)),
            const SizedBox(height: 8),
            Text(
              'Confidence: ${(insight['confidence_score'] * 100).toStringAsFixed(0)}%',
              style: TextStyle(color: Colors.grey[700], fontSize: 13),
            ),
            const SizedBox(height: 4),
            if (insight['reference_rows'] != null)
              Text(
                'Reference Rows: ${insight['reference_rows'].join(', ')}',
                style: TextStyle(color: Colors.grey[600], fontSize: 13),
              ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI-Generated Insights')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: isLoading
            ? const Center(child: CircularProgressIndicator())
            : errorMessage != null
                ? Center(child: Text(errorMessage!, style: const TextStyle(color: Colors.red)))
                : (insights == null || insights!.isEmpty)
                    ? const Center(child: Text('No insights found.'))
                    : ListView.builder(
                        itemCount: insights!.length,
                        itemBuilder: (context, index) =>
                            _buildInsightCard(insights![index]),
                      ),
      ),
    );
  }
}

