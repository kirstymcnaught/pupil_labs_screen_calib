import QtQuick 2.0
import QtQuick.Controls 1.2

Rectangle {
    id: top
    width: 800; height: 800

    function onPupilReady() {
        console.log('pupil is ready!')
    }

    Button {
        id: btn
        anchors.centerIn: parent
        text: "Click to start"
        onClicked: {
//            pupil.start_calib(500,500)

            pupil.start_calib(top.width, top.height)
            circle.visible = true
            btn.visible = false
//            waitTimer.start()
            stimulus.next()
        }
    }

    Rectangle {
        id: stimulus
        width: 50
        height: 50
        x: 50
        y: 50

        property bool started: false

        function next() {
            if (started) {
                x += 250;
            }
            else {
                started = true;
            }

            var x_wrap = x % top.width
            if (x_wrap < x) {
                y += 125;
                x = x_wrap
            }

            var y_wrap = y % top.width
            if (y_wrap < y) {
                console.log('finished')
            }
            else {
                circle.r = 35;
                anim.restart();
            }
        }


        Circle {
            id: circle
            visible: false
            anchors.centerIn: parent
            color: "red"

            property int minWidth: 40
            property int maxWidth: 50
            property int animTime: 250

            SequentialAnimation {
                id: anim

                running: false
                SequentialAnimation {
                    PropertyAnimation { target: circle; property: "r"; to: 20; duration: circle.animTime*2 }
                    PropertyAnimation { target: circle; property: "r"; to: 5; duration: circle.animTime*2 }
                }
                SequentialAnimation {
                    loops: 6 //Animation.Infinite
                    PropertyAnimation { target: circle; property: "r"; to: 15; duration: circle.animTime }
                    PropertyAnimation { target: circle; property: "r"; to: 5; duration: circle.animTime }
                }
                onStopped: {
                    console.log('stimulus complete')
                    stimulus.next()
                }
            }

        }
    }
}
