import React from 'react'
import { View, Text } from 'react-native'
import { styled, withExpoSnack } from 'nativewind'

const StyledView = styled(View)
const StyledText = styled(Text)

const settings = () => {
  return (
    <StyledView className="flex-1 items-center justify-center h-full">
        <StyledText>Settings</StyledText>
    </StyledView>
  )
}

export default withExpoSnack(settings)