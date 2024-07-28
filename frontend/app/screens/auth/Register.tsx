import { View, Text, StatusBar, TextInput, TouchableOpacity } from 'react-native'
import { AuthContext } from '@/context/AuthContext'
import { styled }  from "nativewind"
import React from 'react'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledTextInput = styled(TextInput)
const StyledTouchableOpacity = styled(TouchableOpacity)

const Register = ({route, navigation}: {route: any, navigation: any}) => {
  const [ username, setUsername ] = React.useState<string>('')
  const [ email, setEmail ] = React.useState<string>('')
  const [ password, setPassword ] = React.useState<string>('')
  const [ rePassword, setRePassword ] = React.useState<string>('')

  const { signUp } = React.useContext(AuthContext)

  const { text } = route.params

  const register = () => {

    const message = {username: '', email: '', password: '', rePassword: ''}
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/
    let valid = true

    if (password !== rePassword) {
      message.rePassword = 'Passwords do not match'
      valid = false
    }
    if (password.length < 8) {
      message.password = 'Password must be at least 8 characters'
      valid = false
    }
    if (username.length < 4) {
      message.username = 'Username must be at least 4 characters'
      valid = false
    }
    if (emailRegex.test(email) === false) {
      message.email = 'Invalid email'
      valid = false
    }

    if (!valid)
      navigation.setParams({ text: message })
    else 
      signUp({ username, email, password })
    
  }

  return (
    <>
      <StatusBar barStyle="dark-content" backgroundColor="white" />
      <StyledView className="flex-1 items-center justify-center space-y-2 bg-white">
        <StyledText className="text-xl font-bold">Create an account</StyledText>

        <StyledView className="w-3/4">
          <StyledText className="text-red-500">{text.username}</StyledText>
          <StyledTextInput 
            placeholder="Username" 
            className="w-full h-[45] border-2 border-gray-500 rounded-xl p-2" 
            autoCapitalize='none' 
            value={username} 
            onChangeText={setUsername}
          />
        </StyledView>

        <StyledView className="w-3/4">
          <StyledText className="text-red-500">{text.email}</StyledText>
          <StyledTextInput 
            placeholder="Email" 
            className="w-full h-[45] border-2 border-gray-500 rounded-xl p-2" 
            autoCapitalize='none' 
            value={email} 
            onChangeText={setEmail}
          />
        </StyledView>

        <StyledView className="w-3/4">
          <StyledText className="text-red-500">{text.password}</StyledText>
          <StyledTextInput 
            placeholder="Password" 
            className="w-full h-[45] border-2 border-gray-500 rounded-xl p-2" 
            secureTextEntry 
            autoCapitalize='none' 
            value={password} 
            onChangeText={setPassword}
          />
        </StyledView>

        <StyledView className="w-3/4 mb-5">
          <StyledText className="text-red-500">{text.rePassword}</StyledText>
          <StyledTextInput 
            placeholder="Confirm Password" 
            className="w-full h-[45] border-2 border-gray-500 rounded-xl p-2" 
            secureTextEntry 
            autoCapitalize='none' 
            value={rePassword} 
            onChangeText={setRePassword}
          />
        </StyledView>

        <StyledTouchableOpacity 
          className="bg-blue-500 p-2 rounded-xl w-3/4"
          onPress={() => {register()}}
        >
          <StyledText className="text-white bg-blue-500 rounded-xl text-center text-xl font-bold">Register</StyledText>
        </StyledTouchableOpacity>
      </StyledView>
    </>
  )
}

export default Register