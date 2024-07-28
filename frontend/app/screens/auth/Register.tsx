import { View, Text, StatusBar } from 'react-native'
import React from 'react'

const Register = ({route, navigation}: {route: any, navigation: any}) => {
  const { text } = route.params
  return (
    <View>
      <StatusBar barStyle="dark-content" backgroundColor="#ecf0f1" />
      <Text>{text}</Text>
    </View>
  )
}

export default Register