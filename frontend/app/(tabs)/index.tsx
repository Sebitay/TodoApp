import React from 'react'
import { View, Text } from 'react-native'
import { styled, withExpoSnack } from 'nativewind'

const StyledView = styled(View)
const StyledText = styled(Text)

const index = () => {
  return (
    <StyledView className="flex-1 items-center justify-center h-full">
        <StyledText>Index</StyledText>
    </StyledView>
  )
}

export default withExpoSnack(index)