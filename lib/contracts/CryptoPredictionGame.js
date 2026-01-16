// CryptoPredictionGame Contract Class
// Wrapper for interacting with crypto_prediction_game_realtime.py

import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';

class CryptoPredictionGame {
  constructor(contractAddress, address, studioUrl) {
    this.contractAddress = contractAddress;
    
    const config = {
      chain: studionet,
    };

    if (address) {
      config.account = address;
    }

    this.client = createClient(config);
  }

  // ============================================
  // VIEW FUNCTIONS (Read-only, no gas)
  // ============================================

  /**
   * Get current blockchain time
   */
  async getCurrentTime() {
    try {
      const result = await this.client.readContract({
        address: this.contractAddress,
        functionName: 'get_current_time',
        args: [],
      });
      return result;
    } catch (error) {
      console.error('Error getting current time:', error);
      throw error;
    }
  }

  /**
   * Get current price for a crypto
   */
  async getCurrentPrice(symbol) {
    try {
      const result = await this.client.readContract({
        address: this.contractAddress,
        functionName: 'get_current_price',
        args: [symbol],
      });
      return result;
    } catch (error) {
      console.error('Error getting price:', error);
      throw error;
    }
  }

  /**
   * Get user balance
   */
  async getBalance(userAddress) {
    try {
      const result = await this.client.readContract({
        address: this.contractAddress,
        functionName: 'get_balance',
        args: [userAddress],
      });
      return result;
    } catch (error) {
      console.error('Error getting balance:', error);
      throw error;
    }
  }

  /**
   * Get prediction details
   */
  async getPredictionDetails(predictionId) {
    try {
      const result = await this.client.readContract({
        address: this.contractAddress,
        functionName: 'get_prediction_details',
        args: [predictionId],
      });
      return result;
    } catch (error) {
      console.error('Error getting prediction details:', error);
      throw error;
    }
  }

  /**
   * Get user predictions summary
   */
  async getUserPredictions(userAddress) {
    try {
      const result = await this.client.readContract({
        address: this.contractAddress,
        functionName: 'get_user_predictions',
        args: [userAddress],
      });
      return result;
    } catch (error) {
      console.error('Error getting user predictions:', error);
      throw error;
    }
  }

  /**
   * Get user active predictions with details
   */
  async getUserActivePredictions(userAddress) {
    try {
      const result = await this.client.readContract({
        address: this.contractAddress,
        functionName: 'get_user_active_predictions',
        args: [userAddress],
      });
      return result;
    } catch (error) {
      console.error('Error getting active predictions:', error);
      throw error;
    }
  }

  /**
   * Get leaderboard
   */
  async getLeaderboard() {
    try {
      const result = await this.client.readContract({
        address: this.contractAddress,
        functionName: 'get_leaderboard',
        args: [],
      });
      return result;
    } catch (error) {
      console.error('Error getting leaderboard:', error);
      throw error;
    }
  }

  /**
   * Get game statistics
   */
  async getGameStats() {
    try {
      const result = await this.client.readContract({
        address: this.contractAddress,
        functionName: 'get_game_stats',
        args: [],
      });
      return result;
    } catch (error) {
      console.error('Error getting game stats:', error);
      throw error;
    }
  }

  // ============================================
  // WRITE FUNCTIONS (Transactions, costs gas)
  // ============================================

  /**
   * Deposit tokens
   */
  async deposit(userAddress, amount) {
    try {
      const txHash = await this.client.writeContract({
        address: this.contractAddress,
        functionName: 'deposit',
        args: [userAddress, amount],
        value: BigInt(0),
      });

      const receipt = await this.client.waitForTransactionReceipt({
        hash: txHash,
        status: 'ACCEPTED',
        retries: 24,
        interval: 5000,
      });

      return receipt;
    } catch (error) {
      console.error('Error depositing:', error);
      throw error;
    }
  }

  /**
   * Place a prediction
   */
  async placePrediction(userAddress, symbol, direction, betAmount, durationSeconds) {
    try {
      const txHash = await this.client.writeContract({
        address: this.contractAddress,
        functionName: 'place_prediction',
        args: [userAddress, symbol, direction, betAmount, durationSeconds],
        value: BigInt(0),
      });

      const receipt = await this.client.waitForTransactionReceipt({
        hash: txHash,
        status: 'ACCEPTED',
        retries: 24,
        interval: 5000,
      });

      return receipt;
    } catch (error) {
      console.error('Error placing prediction:', error);
      throw error;
    }
  }

  /**
   * Settle a prediction
   */
  async settlePrediction(userAddress, predictionId) {
    try {
      const txHash = await this.client.writeContract({
        address: this.contractAddress,
        functionName: 'settle_prediction',
        args: [userAddress, predictionId],
        value: BigInt(0),
      });

      const receipt = await this.client.waitForTransactionReceipt({
        hash: txHash,
        status: 'ACCEPTED',
        retries: 24,
        interval: 5000,
      });

      return receipt;
    } catch (error) {
      console.error('Error settling prediction:', error);
      throw error;
    }
  }
}

export default CryptoPredictionGame;
