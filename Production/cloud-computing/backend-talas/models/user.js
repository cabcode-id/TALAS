'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class User extends Model {
    static associate(models) {
      // define association here
    }
  }
  User.init({
    id:{
      allowNull: false,
      autoIncrement: true,
      primaryKey: true,
      type: DataTypes.INTEGER
    },
    username: DataTypes.STRING,
    email:{
      unique: true,
      type: DataTypes.STRING,
    },
    password: DataTypes.STRING,
    hp: DataTypes.STRING,
    role: {
      type: DataTypes.ENUM,
      values: ['admin', 'umum']
    }
  }, {
    sequelize,
    modelName: 'User',
  });
  return User;
};