import { View, Text, TouchableOpacity } from 'react-native'
import { Icon } from 'rn-inkpad'
import { styled }  from "nativewind"
import React from 'react'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledTouchableOpacity = styled(TouchableOpacity)

const TodoListItem = ({text, id}: {text:string, id:number}) => {
  const [checked, setChecked] = React.useState<boolean>(false)
  return (
    <StyledView className="flex-row border-y-[1px] border-gray-200 items-center">
        <StyledTouchableOpacity className="flex-1 p-1 pl-3 grow-0" onPress={() => setChecked(!checked)}>
        {checked ? (
          <Icon name="checkmark-circle" size={30} color="slate" />
        ) : (
          <Icon name="ellipse-outline" size={30} color="slate" />
        )}
        </StyledTouchableOpacity>
        <StyledTouchableOpacity className="flex-1 p-2">
            <StyledText className='text-base'>{text}</StyledText>
        </StyledTouchableOpacity>
    </StyledView>
  )
}

export default TodoListItem