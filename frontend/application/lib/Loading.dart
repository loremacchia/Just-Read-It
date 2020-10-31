import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class Loading extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black54,
      child: Semantics(
        label: "Searching for the text into the image",
        child: Center(
          child: SpinKitCircle(
            color: Colors.white,
            size: 75.0,
          ),
        ),
      ),
    );
  }
}
