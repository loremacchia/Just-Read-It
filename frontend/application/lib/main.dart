import 'dart:convert';
import 'dart:ui';
import 'dart:async';
import 'dart:io';
import 'dart:collection';

import 'package:flutter/gestures.dart';
import 'package:http/http.dart' as http;
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart' show join;
import 'package:path_provider/path_provider.dart';
import 'package:sliding/Loading.dart';
import 'package:sliding_up_panel/sliding_up_panel.dart';
import 'package:sliding/GridElementRound.dart';
import 'package:string_validator/string_validator.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  final firstCamera = cameras.first;
  Scaffold.shouldSnackBarIgnoreFABRect = true;

  runApp(SlidingUpPanelExample(camera: firstCamera));
}

class SlidingUpPanelExample extends StatelessWidget {
  final CameraDescription camera;

  SlidingUpPanelExample({this.camera});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Just Read It',
        theme: ThemeData(fontFamily: 'San Francisco'),
        home: Scaffold(
          body: HomePage(
            //url: "http://7d2969e85c64.ngrok.io",
            camera: camera,
          ),
        ));
  }
}

class HomePage extends StatefulWidget {
  final CameraDescription camera;
  //final String url;

  //HomePage({Key key, this.camera, this.url}) : super(key: key);
  HomePage({Key key, this.camera}) : super(key: key);
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String url;

  final double _initFabHeight = 120.0;
  double _fabHeight;
  double _panelHeightOpen;
  double _panelHeightClosed = 84.0;

  CameraController _controller;
  Future<void> _initializeControllerFuture;
  String imgPath;
  bool isLoading = false;

  LinkedHashMap grid;
  List<GridElementRound> list;
  int newWords = 0;
  List<String> threeWords;
  double _bodyOpacity = 1;
  double _gridOpacity = 1;

  @override
  void initState() {
    super.initState();
    //Headset.speak("");

    _controller = CameraController(
      widget.camera,
      ResolutionPreset.high,
    );
    _initializeControllerFuture = _controller.initialize();

    _fabHeight = _initFabHeight;
    resetInterface();
  }

  void resetInterface(){
    grid = new LinkedHashMap<String, List<String>>();

    grid["Top Left"] = [""];
    grid["Top"] = [""];
    grid["Top Right"] = [""];
    grid["Center Left"] = [""];
    grid["Center"] = [""];
    grid["Center Right"] = [""];
    grid["Bottom Left"] = [""];
    grid["Bottom"] = [""];
    grid["Bottom Right"] = [""];
    list = [];
    grid.entries.forEach((e) => {
      list.add(new GridElementRound(
        position: e.key,
        words: e.value,
      )),
    });
    threeWords = ["", "", ""];
  }

  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void updateText(
      Map<String, dynamic> dictGrid, List listThreeWords, int numWords) {
    for (final key in dictGrid.keys) {
      print(key);
      grid[key] = List<String>.from(dictGrid[key]);
    }

    list = [];
    grid.entries.forEach((e) => {
          list.add(new GridElementRound(
            position: e.key,
            words: e.value,
          )),
        });
    threeWords = List<String>.from(listThreeWords);
    newWords = numWords;
  }

  Future<http.Response> uploadImage(filename) async {
    //var request = http.MultipartRequest('POST', Uri.parse(widget.url));
    var request = http.MultipartRequest('POST', Uri.parse(url));
    request.files.add(await http.MultipartFile.fromPath('image', filename));
    var streamedRes = await request.send();
    var res = http.Response.fromStream(streamedRes);
    return res;
  }

  @override
  Widget build(BuildContext context) {
    _panelHeightOpen = MediaQuery.of(context).size.height * .80;
    return Material(
      color: Colors.black87,
      child: Stack(
        alignment: Alignment.topCenter,
        children: <Widget>[
          SlidingUpPanel(
            maxHeight: _panelHeightOpen,
            minHeight: _panelHeightClosed,
            parallaxEnabled: true,
            parallaxOffset: .5,
            body: _body(),
            panelBuilder: (sc) => _panel(sc),
            borderRadius: BorderRadius.only(
                topLeft: Radius.circular(14.0),
                topRight: Radius.circular(14.0)),
            onPanelSlide: (double pos) => setState(() {
              pos == 0
                  ? _bodyOpacity = 1
                  : _bodyOpacity = (1 - pos) * 0.5 + 0.5;
              _fabHeight = pos * (_panelHeightOpen - _panelHeightClosed) +
                  _initFabHeight;
            }),
          ),
        ],
      ),
    );
  }

  Widget _panel(ScrollController sc) {
    return MediaQuery.removePadding(
        context: context,
        removeTop: true,
        child: ListView(
          controller: sc,
          children: <Widget>[
            SizedBox(
              height: 10.0,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Container(
                  width: 30,
                  height: 5,
                  decoration: BoxDecoration(
                      color: const Color(0xff345a99),
                      borderRadius: BorderRadius.all(Radius.circular(12.0))),
                ),
              ],
            ),
            SizedBox(
              height: 7.0,
            ),
            Container(
              decoration: BoxDecoration(
                  border: Border(
                      bottom: BorderSide(
                width: 0.3,
                color: Colors.black26,
              ))),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text(
                    "Read Text Inside Image",
                    style: TextStyle(
                      fontWeight: FontWeight.normal,
                      fontSize: 22.0,
                    ),
                  ),
                  SizedBox(
                    height: 5.0,
                  ),
                  Text(
                    "There are $newWords new words",
                    style: TextStyle(
                      fontWeight: FontWeight.w200,
                      fontSize: 18.0,
                    ),
                  ),
                  SizedBox(
                    height: 10.0,
                  ),
                ],
              ),
            ),
            /*SizedBox(
              height: 36.0,
            ),
            */
            SizedBox(
              height: 10.0,
            ),
            AnimatedOpacity(
              opacity: _gridOpacity,
              duration: const Duration(milliseconds: 300),
              child: Semantics(
                label: "Text of the image",
                child: GridView.count(
                  shrinkWrap: true,
                  crossAxisCount: 3,
                  children: list.map((e) => e).toList(),
                ),
              ),
            ),
          ],
        ));
  }

  Widget _body() {
    return AnimatedOpacity(
      duration: const Duration(milliseconds: 300),
      opacity: _bodyOpacity,
      child: Container(
        constraints: BoxConstraints.expand(
          height: MediaQuery.of(context).size.height - _panelHeightClosed,
        ),
        alignment: Alignment.topCenter,
        decoration: BoxDecoration(
          color: const Color(0xffe0e7f2),
          image: DecorationImage(
            image: (imgPath == null)
                ? Image.asset("images/Wallpaper.png").image
                : Image.file(File("$imgPath")).image,
            fit: BoxFit.fill,
          ),
        ),
        child: isLoading
            ? Loading()
            : Padding(
                padding: EdgeInsets.fromLTRB(0, 0, 0, _panelHeightClosed + 5),
                child: Align(
                  alignment: Alignment.bottomCenter,
                  child: Padding(
                    padding:
                        EdgeInsets.symmetric(vertical: 10.0, horizontal: 10.0),
                    child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: <Widget>[
                          RawMaterialButton(
                            onPressed: () => onPressURL(),
                            elevation: 2.0,
                            fillColor: Colors.white,
                            child: Text(
                              "URL",
                              style: TextStyle(
                                fontWeight: FontWeight.w800,
                                color: const Color(0xff345a99),
                              ),
                            ),
                            padding: EdgeInsets.all(17.0),
                            shape: CircleBorder(),
                          ),
                          RawMaterialButton(
                            onPressed: () async {
                              String path;
                              path = await shotPic();
                              setState(() {
                                resetInterface();
                                isLoading = true;
                                imgPath = path;
                              });
                              if (isURL(url)) {
                                final resp = await uploadImage(imgPath);
                                if (resp.statusCode == 200) {
                                  final Map parsed = json.decode(resp.body);
                                  Scaffold.of(context).showSnackBar(
                                      snackBarText(
                                          parsed["threeWords"] as List));
                                  setState(() {
                                    isLoading = false;
                                    imgPath = path;
                                    updateText(
                                        parsed["grid"] as Map,
                                        parsed["threeWords"] as List,
                                        parsed["newWords"] as int);
                                  });
                                } else {
                                  Scaffold.of(context)
                                      .showSnackBar(snackBarError("Request is not valid"));
                                  setState(() {
                                    resetInterface();
                                    isLoading = false;
                                  });
                                }
                              } else {
                                Scaffold.of(context)
                                    .showSnackBar(snackBarError("Check server URL!"));
                                setState(() {
                                  resetInterface();
                                  isLoading = false;
                                });
                              }
                            },
                            elevation: 2.0,
                            fillColor: const Color(0xff345a99),
                            child: Icon(
                              Icons.add_a_photo,
                              size: 34.0,
                              color: Colors.white,
                              semanticLabel: "Take a photo to read its content",
                            ),
                            padding: EdgeInsets.all(17.0),
                            shape: CircleBorder(),
                          )
                        ]),
                  ),
                ),
              ),
      ),
    );
  }

  void onPressURL(){
    TextEditingController customController =
    TextEditingController();
    showDialog(
        context: context,
        builder: (context) {
          return AlertDialog(
            title: Text("Insert the server URL"),
            content: TextField(
              controller: customController,
            ),
            actions: <Widget>[
              MaterialButton(
                onPressed: () {
                  Navigator.of(context).pop(
                      customController.text
                          .toString());
                },
                child: Text("Submit"),
                elevation: 2.0,
              )
            ],
          );
        }).then((value) => setState(() {
      print(value);
      url = value;
      print(url);
    }));
  }
  Widget snackBarError(String string) {
    return SnackBar(
        backgroundColor: const Color(0xffC61E07),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(20.0)),
        ),
        content: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            Text(
              string,
              style: TextStyle(
                fontWeight: FontWeight.w400,
                fontSize: 18.0,
                color: Colors.white,
              ),
            ),
          ],
        ));
  }

  Widget snackBarText(List list) {
    return SnackBar(
      backgroundColor: const Color(0xffdcdee5),
      behavior: SnackBarBehavior.floating,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(20.0)),
      ),
      content: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8.0),
        child: Semantics(
          label: "Three most important words",
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: list.map((e) => threeText(e)).toList(),
          ),
        ),
      ),
    );
  }

  Widget threeText(String text) {
    return Container(
      decoration: BoxDecoration(
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.7),
            spreadRadius: 1,
            blurRadius: 3,
            offset: Offset(0, 3), // changes position of shadow
          ),
        ],
        color: const Color(0xff345a99),
        borderRadius: BorderRadius.all(
            Radius.circular(30.0) //         <--- border radius here
            ),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 2.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              text,
              style: TextStyle(
                fontWeight: FontWeight.w300,
                fontSize: 18.0,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<String> shotPic() async {
    String path = "";
    try {
      await _initializeControllerFuture;
      path = join(
        (await getApplicationDocumentsDirectory()).path,
        '${DateTime.now()}.png',
      );
      await _controller.takePicture(path);
      print(path);
    } catch (e) {
      print(e);
    }
    return path;
  }
}
