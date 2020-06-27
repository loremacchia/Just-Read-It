import 'package:flutter/material.dart';

class GridElementRound extends StatefulWidget {
  String position;
  List<String> words;
  GridElementRound({this.position, this.words});

  @override
  _GridElementRoundState createState() => _GridElementRoundState();
}

class _GridElementRoundState extends State<GridElementRound> {
  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: (){
        if(widget.words.length > 3){
          showDialog(
            context: context,
            builder: (context) {
              return Dialog(
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(40)),
                  elevation: 5,
                  child: boxDialog(widget.position, widget.words)
              );
            },
          );
        }
      },
      child: Padding(
        padding: const EdgeInsets.all(6.0),
        child: Container(
          decoration: BoxDecoration(
            color: const Color(0xff345a99),
            borderRadius: BorderRadius.all(
                Radius.circular(12.0) //         <--- border radius here
                ),
            border: Border.all(
              width: 0.15,
              color: const Color(0xff3D88A7),
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.7),
                spreadRadius: 2,
                blurRadius: 4,
                offset: Offset(0, 3), // changes position of shadow
              ),
            ],
          ),
          child: Padding(
            padding: const EdgeInsets.all(4.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                Container(
                  decoration: BoxDecoration(
                    border: Border(
                      bottom: BorderSide(
                        width: 1,
                        color: const Color(0xff5da6c1),)
                    ),
                  ),
                  child: Text(
                    widget.position,
                    style: TextStyle(
                      fontWeight: FontWeight.w500,
                      fontSize: 17.0,
                      color: Colors.white,
                    ),
                  ),
                ),
                SizedBox(
                  height: 5.0,
                ),
                if (widget.words.length > 0 && widget.words.length <= 3)
                  Column(
                      children: widget.words
                          .map((word) => Text(
                        word,
                        style: TextStyle(
                          fontSize: 16.0,
                          color: Colors.white,
                          fontWeight: FontWeight.w200,
                        ),
                      ))
                          .toList())
                else if (widget.words.length > 3)
                  Column(
                      children: widget.words.sublist(1,4)
                          .map((word) => Text(
                        word,
                        style: TextStyle(
                          fontSize: 16.0,
                          color: Colors.white,
                          fontWeight: FontWeight.w200,
                        ),
                      ))
                          .toList())
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget boxDialog(String position, List<String> words){
    return Container(
      padding: const EdgeInsets.all(6.0),
      decoration: BoxDecoration(
        color: const Color(0xff345a99),
        borderRadius: BorderRadius.all(
            Radius.circular(12.0) //         <--- border radius here
        ),
        border: Border.all(
          width: 0.15,
          color: const Color(0xff3D88A7),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.7),
            spreadRadius: 2,
            blurRadius: 4,
            offset: Offset(0, 3), // changes position of shadow
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(4.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            Container(
              decoration: BoxDecoration(
                border: Border(
                    bottom: BorderSide(
                      width: 1,
                      color: const Color(0xff5da6c1),
                    )),
              ),
              child: Text(
                position,
                style: TextStyle(
                  fontWeight: FontWeight.w400,
                  fontSize: 24.0,
                  color: Colors.white,
                ),
              ),
            ),
            SizedBox(
              height: 5.0,
            ),
            Column(
                children: words
                    .map((word) => Text(
                  word,
                  style: TextStyle(
                    fontSize: 20.0,
                    color: Colors.white,
                    fontWeight: FontWeight.w200,
                  ),
                ))
                    .toList())
          ],
        ),
      ),
    );
  }
}
