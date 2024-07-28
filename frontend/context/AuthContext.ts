import * as React from 'react';

export const AuthContext = React.createContext({signOut: () => {}, signIn: ({username, password}: {username:string, password: string}) => {console.log(username, password)}, signUp: () => {}});