import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialIcons';
import messaging from '@react-native-firebase/messaging';
import axios from 'axios';

// Import Screens
import HomeScreen from './src/screens/HomeScreen';
import GlucoseScreen from './src/screens/GlucoseScreen';
import GamesScreen from './src/screens/GamesScreen';
import ProfileScreen from './src/screens/ProfileScreen';
import TicTacToe from './src/screens/games/TicTacToe';
import RockPaperScissors from './src/screens/games/RockPaperScissors';
import ProfileSettings from './src/screens/ProfileSettings';
import Auth from './src/screens/authentication/Auth';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Fetch Instagram Data in the Background
const fetchInstagramData = async () => {
  try {
    await axios.get("http://10.0.2.2:5000/instagram/analyze-instagram-emotion");
  } catch (error) {
    console.error("Instagram Fetch Error:", error);
  }
};

const App = () => {
  useEffect(() => {
    // Request Firebase Notification Permission
    messaging().requestPermission();

    // Listen for Firebase Notifications (Instagram & In-App Feed)
    const unsubscribe = messaging().onMessage(async (remoteMessage) => {
      console.log("Notification Received:", remoteMessage);
      alert(` ${remoteMessage.notification?.title} - ${remoteMessage.notification?.body}`);
    });

    // Run Instagram Fetch in the Background Every 10 Seconds
    const interval = setInterval(fetchInstagramData, 10000);

    return () => {
      unsubscribe();
      clearInterval(interval);
    };
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Auth" component={Auth} /> 
        <Stack.Screen name="Main" component={BottomTabNavigator} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

// Games Stack
const GamesStack = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Games" component={GamesScreen} />
    <Stack.Screen name="TicTacToe" component={TicTacToe} />
    <Stack.Screen name="RockPaperScissors" component={RockPaperScissors} />
  </Stack.Navigator>
);

// Bottom Tabs with Profile Stack
const BottomTabNavigator = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      tabBarIcon: ({ color, size }) => {
        let iconName;
        if (route.name === 'Home') iconName = 'home';
        else if (route.name === 'Glucose') iconName = 'show-chart';
        else if (route.name === 'Games') iconName = 'sports-esports';
        else if (route.name === 'Profile') iconName = 'person';

        return <Icon name={iconName} size={size} color={color} />;
      },
      tabBarActiveTintColor: '#7BCCD4',
      tabBarInactiveTintColor: 'gray',
      headerShown: false,
    })}
  >
    <Tab.Screen name="Home" component={HomeScreen} />
    <Tab.Screen name="Glucose" component={GlucoseScreen} />
    <Tab.Screen name="Games" component={GamesStack} />
    <Tab.Screen name="Profile" component={ProfileStack} options={{ title: 'Profile' }} />
  </Tab.Navigator>
);

// Profile Stack
const ProfileStack = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Profile" component={ProfileScreen} />
    <Stack.Screen name="ProfileSettings" component={ProfileSettings} />
  </Stack.Navigator>
);

export default App;
