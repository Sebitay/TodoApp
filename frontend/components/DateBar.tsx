import { View, Text, TouchableOpacity } from 'react-native'
import DateTimePicker from 'react-native-ui-datepicker';
import { styled }  from "nativewind"
import { Icon } from 'rn-inkpad'
import React from 'react'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledTouchableOpacity = styled(TouchableOpacity)

const DateBar = ({date, setDate}: {date: Date, setDate: any}) => {

    const [open, setOpen] = React.useState<boolean>(false)

    const prevDate = () => {
        setDate(new Date(date.getFullYear(), date.getMonth(), date.getDate()-1))
    }

    const nextDate = () => {
        setDate(new Date(date.getFullYear(), date.getMonth(), date.getDate()+1))
    }
    
    return (
        <StyledView className="flex-row items-center justify-between py-4 px-2 bg-white">
            <StyledTouchableOpacity onPress={() => {prevDate()}} className='flex-row'>
                <Icon name="chevron-back" size={30} color="slate" />
                <StyledText className="text-xl">Prev</StyledText>
            </StyledTouchableOpacity>
            <StyledTouchableOpacity onPress={() => {setOpen(!open)}} className='flex-row'>
                <StyledText className="text-xl font-bold">{date.toLocaleDateString('default', {day: 'numeric', month: 'long', weekday: 'short'})}</StyledText>
            </StyledTouchableOpacity>
            <StyledTouchableOpacity onPress={() => {nextDate()}} className='flex-row'>
                <StyledText className="text-xl">Next</StyledText>
                <Icon name="chevron-forward" size={30} color="slate" />
            </StyledTouchableOpacity>
        </StyledView>
    )
}

export default DateBar