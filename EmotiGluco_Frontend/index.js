/**
 * @format
 */
import { AppRegistry } from 'react-native';
import messaging from '@react-native-firebase/messaging';
import App from './App';
import { name as appName } from './app.json';

// ✅ Request user permission for notifications
async function requestUserPermission() {
    const authStatus = await messaging().requestPermission();
    const enabled =
        authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
        authStatus === messaging.AuthorizationStatus.PROVISIONAL;

    if (enabled) {
        console.log('✅ Notification permission granted.');
        await getFCMToken();
    }
}

// ✅ Get FCM Token
async function getFCMToken() {
    try {
        const token = await messaging().getToken();
        console.log("🔥 FCM Token:", token);
    } catch (error) {
        console.error("❌ Error getting FCM token", error);
    }
}

// ✅ Handle foreground push notifications
messaging().onMessage(async remoteMessage => {
    console.log("📩 Foreground Notification:", remoteMessage);
    alert(`📩 Notification: ${remoteMessage.notification?.title} - ${remoteMessage.notification?.body}`);
});

// ✅ Handle background push notifications
messaging().setBackgroundMessageHandler(async remoteMessage => {
    console.log("📩 Background Notification:", remoteMessage);
});

// ✅ Request permission when app loads
requestUserPermission();

AppRegistry.registerComponent(appName, () => App);
