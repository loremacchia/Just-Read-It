import 'package:flutter/animation.dart';
import 'package:flutter/material.dart';

class GridElement extends StatefulWidget {
  String position;
  List<String> words;

  GridElement({this.position, this.words});

  @override
  _GridElementState createState() => _GridElementState();
}

class _GridElementState extends State<GridElement> {
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
          color: Colors.white,
          border: Border(
            bottom: BorderSide(
              width: 0.25,
              color: const Color(0xff1565c0),
            ),
            left: BorderSide(
              width: 0.1,
              color: const Color(0xff1565c0),
            ),
            right: BorderSide(
              width: 0.1,
              color: const Color(0xff1565c0),
            ),
          )),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          Text(
            widget.position,
            style: TextStyle(
              fontWeight: FontWeight.normal,
              fontSize: 18.0,
              color: Colors.black87,
            ),
          ),
          SizedBox(
            height: 5.0,
          ),
          if (widget.words.length > 0)
            Column(
                children: widget.words
                    .map((word) => Text(
                          word,
                          style: TextStyle(
                            fontSize: 18.0,
                            color: Colors.black87,
                            fontWeight: FontWeight.w300,
                          ),
                        ))
                    .toList())
        ],
      ),
    );
  }
}
