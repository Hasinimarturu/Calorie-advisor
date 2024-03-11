import React from 'react';
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Alert, View, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import Login from "./components/Login";
import History from "./components/History";
import Signup from "./components/Signup";
import CalorieAdvisor from './components/CalorieAdvisor';

import { MaterialIcons } from '@expo/vector-icons';
import { MaterialCommunityIcons } from '@expo/vector-icons';

const App = ({ navigation }) => { // Pass navigation prop
  const Tab = createBottomTabNavigator();

  const handleLogout = async () => {
    await AsyncStorage.clear();
    Alert.alert('Logout', 'You have been successfully logged out');
    // Navigate to the Login screen
    // navigation.navigate('Login');
  };

  return (   
    <View style={{ flex: 1 }}>
      <NavigationContainer>
        <Tab.Navigator>
          <Tab.Screen name="Login" component={Login} options={
            { tabBarIcon: () => <MaterialIcons name="login" size={24} color="black" /> }
          } />
          <Tab.Screen name="Register" component={Signup} options={
            { tabBarIcon: () => <MaterialCommunityIcons name="registered-trademark" size={24} color="black" /> }
          } />
          <Tab.Screen name="CalorieAdvisor" component={CalorieAdvisor} options={
            { tabBarIcon: () => <MaterialIcons name="chat" size={24} color="black" /> }
          } />
          <Tab.Screen name="History" component={History} options={
            { tabBarIcon: () => <MaterialIcons name="history" size={24} color="black" /> }
          } />
        </Tab.Navigator>
      </NavigationContainer>
      <View>
        <Button title="Logout" onPress={handleLogout} />
      </View>
    </View>
  );
};

export default App;
