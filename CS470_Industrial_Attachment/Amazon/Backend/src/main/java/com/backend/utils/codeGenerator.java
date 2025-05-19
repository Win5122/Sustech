package com.backend.utils;


import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.generator.AutoGenerator;
import com.baomidou.mybatisplus.generator.config.DataSourceConfig;
import com.baomidou.mybatisplus.generator.config.GlobalConfig;
import com.baomidou.mybatisplus.generator.config.PackageConfig;
import com.baomidou.mybatisplus.generator.config.StrategyConfig;
import com.baomidou.mybatisplus.generator.config.rules.NamingStrategy;

public class codeGenerator {
    public static void main(String[] args) {
        // 1、创建代码生成器
        AutoGenerator mpg = new AutoGenerator();

        // 2、全局配置
        // 全局配置
        GlobalConfig gc = new GlobalConfig();
        // TODO:设置生成文件的输出目录
        gc.setOutputDir("D:\\Amazon\\Backend" + "/src/main/java");
        //去掉Service接口的首字母I
        gc.setServiceName("%sService");
        // TODO:设置作者
        gc.setAuthor("wqy");
        gc.setOpen(false);
        mpg.setGlobalConfig(gc);

        // 3、数据源配置
        DataSourceConfig dsc = new DataSourceConfig();
        // TODO:设置数据库连接信息
        dsc.setUrl("jdbc:mysql://localhost:3306/se_project");
        dsc.setDriverName("com.mysql.cj.jdbc.Driver");
        dsc.setUsername("se");
        dsc.setPassword("se_project_7777777");
        dsc.setDbType(DbType.MYSQL);
        mpg.setDataSource(dsc);

        // 4、包配置
        PackageConfig pc = new PackageConfig();
        // 模块名
        //pc.setModuleName("sys");
        // TODO:设置包名
        pc.setParent("com.backend.global");
        pc.setController("controller");
        pc.setService("service");
        pc.setMapper("mapper");
        mpg.setPackageInfo(pc);

        // 5、策略配置
        StrategyConfig strategy = new StrategyConfig();
        // TODO:需要生成的表名        strategy.setInclude("global");
        // 数据库表映射到实体的命名策略
        strategy.setNaming(NamingStrategy.underline_to_camel);
        // 数据库表字段映射到实体的命名策略
        strategy.setColumnNaming(NamingStrategy.underline_to_camel);
        // lombok 模型 @Accessors(chain = true) setter链式操作
        strategy.setEntityLombokModel(true);
        // restful api风格控制器
        strategy.setRestControllerStyle(true);
        // url中驼峰转连字符
        strategy.setControllerMappingHyphenStyle(true);
        // MPJ对应的mapper作为父类
        strategy.setSuperMapperClass("com.github.yulichang.base.MPJBaseMapper");
        // 设置策略
        mpg.setStrategy(strategy);

        // 6、执行
        mpg.execute();
    }
}

