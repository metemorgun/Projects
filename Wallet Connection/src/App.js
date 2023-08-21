import React, { useEffect, useState } from 'react';
import Web3 from 'web3';
import ABI from './Abi.json';
import './App.css';

function App() {
  const [account, setAccount] = useState([]);
  const [smartContract, setSmartContract] = useState(null);
  const [readingData, setReadData] = useState('');
  const [amount, setAmount] = useState('');
  const [address, setAddress] = useState('');
  const web3 = new Web3(Web3.givenProvider || 'https://goerli.infura.io/v3/SENIN_INFURA_API');

  const connectWallet = async () => {
    if (window.ethereum) {
      try {
        await window.ethereum.request({ method: 'eth_requestAccounts' });

        const accounts = await web3.eth.getAccounts();
        const message = 'Welcome Do You Want To Connect To This Website?';
        await web3.eth.personal.sign(message, accounts[0], '');

        setAccount(accounts);
      } catch (error) {
        console.log(error);
      }
    } else {
      alert('Please install Metamask');
    }
  };

  const connectContract = async () => {
    try {
      const contractABI = ABI;
      const contractAddress = '0x69020ab37a5BA9472F1f98A590c905038a58ad2A';

      const contract = new web3.eth.Contract(contractABI, contractAddress);
      setSmartContract(contract);
    } catch (error) {
      console.log(error);
    }
  };

  const readData = async () => {
    if (smartContract) {
      try {
        const result = await smartContract.methods.name().call();
        setReadData(result);
      } catch (error) {
        console.log(error);
      }
    } else {
      alert('Failed to Load the Contract');
    }
  };

  const printData = async () => {
    if (smartContract) {
      try {
        const isValidAddress = web3.utils.isAddress(address);
        if (!isValidAddress) {
          alert('Invalid Ethereum address');
          return;
        }

        const value = web3.utils.toWei(amount, 'ether');
        await smartContract.methods.transfer(address, value).send({ from: account[0] });
      } catch (error) {
        console.log('Error sending transaction:', error);
      }
    } else {
      alert('Failed to Load the Contract');
    }
  };

  useEffect(() => {
    connectContract();
  }, []);

  return (
    <div className="App">
      <div className='main-container' >
        <p>Hello</p>
        {
          account.length > 0 ? (
            <div className='box-container' >
              <p>Connected Account: {account[0]}</p>
              <p>Symbol: {readingData}</p>
              <button onClick={readData} >Read Data</button>

              <input className='input-container' type='text' value={amount} onChange={(e) => setAmount(e.target.value)} placeholder='Amount' />
              <input className='input-container' type='text' value={address} onChange={(e) => setAddress(e.target.value)} placeholder='Address' />
              <button onClick={printData} >Print Data</button>
            </div>

          ) : (
            <button onClick={connectWallet} >Connect Wallet</button>
          )
        }
      </div>
    </div>
  );
}

export default App;