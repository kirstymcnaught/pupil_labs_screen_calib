import QtQuick 2.0
import QtQuick.Controls 1.2

Rectangle {
    id: top
    width: 600; height: 600

    Text {
        id: txtComplete
        visible: false
        text: "Calibration complete"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: btn.top
        anchors.bottomMargin: 50
    }

    Button {
        id: btn
        anchors.centerIn: parent
        text: "Click to start calibration"
        onClicked: {
            pupil.start_calib(top.width, top.height)
            stimulus.next()

            circle.visible = true
            btn.visible = false
            txtComplete.visible = false
        }
    }

    Rectangle {
        id: stimulus
        width: 50
        height: 50
        x: xDiff/2
        y: yDiff/2

        property int numStimPerRowOrCol: 3
        property int xDiff: top.width/numStimPerRowOrCol
        property int yDiff: top.height/numStimPerRowOrCol

        property bool started: false

        function next() {
            if (started) {
                x += xDiff;
            }
            else {
                started = true;
            }

            var x_wrap = x % top.width
            if (x_wrap < x) {
                y += yDiff;
                x = xDiff/2
            }

            var y_wrap = y % top.width
            if (y_wrap < y) {
                console.log('finished')
                pupil.finish_calib()
                txtComplete.visible = true
                btn.visible = true
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

            // Animation controls the stimulus presentation, once it's complete
            // we record gaze position for calibration.
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
                    pupil.add_current_point_to_calib(stimulus.x, stimulus.y)
                    stimulus.next()
                }
            }

        }
    }
}
