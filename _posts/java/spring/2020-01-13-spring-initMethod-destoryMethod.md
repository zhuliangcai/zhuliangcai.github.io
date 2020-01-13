---
layout: post
title: spring初始化和销毁方法
categories: [java,spring]
description: spring初始化和销毁方法
keywords: java,spring
---

Spring的 init-method，destroy-method的实现方式？

## init-method

在bean工厂doCreateBean方法中调用initializeBean，在该方法中又调用invokeInitMethods，然后找到BeanDefinition中的mbd.getInitMethodName()获取init-method指定的方法名称进行反射调用

## destroy-method

AbstractBeanFactory中有destroyBean容器关闭前的统一销毁方法，顺次调用使用new DisposableBeanAdapter初始化并调用的destory方法，该对象初始化时会找到String destroyMethodName = inferDestroyMethodIfNecessary(bean, beanDefinition);String destroyMethodName = beanDefinition.getDestroyMethodName();
这里就是在xml或注解定义的destroy-method方法，然后destory方法中反射调用这个销毁方法执行

##  必备知识点 BeanDefinition

```java
public abstract class AbstractBeanDefinition extends BeanMetadataAttributeAccessor
		implements BeanDefinition, Cloneable {
	
	@Nullable
	private String initMethodName; //记录初始化方法

	@Nullable
	private String destroyMethodName;//记录销毁方法
}

//spring bean 工厂
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory
		implements AutowireCapableBeanFactory {
	
	//反射调用初始化方法
	protected void invokeInitMethods(String beanName, final Object bean, @Nullable RootBeanDefinition mbd)
			throws Throwable {

		boolean isInitializingBean = (bean instanceof InitializingBean);
		if (isInitializingBean && (mbd == null || !mbd.isExternallyManagedInitMethod("afterPropertiesSet"))) {
			if (logger.isTraceEnabled()) {
				logger.trace("Invoking afterPropertiesSet() on bean with name '" + beanName + "'");
			}
			if (System.getSecurityManager() != null) {
				try {
					AccessController.doPrivileged((PrivilegedExceptionAction<Object>) () -> {
						((InitializingBean) bean).afterPropertiesSet();
						return null;
					}, getAccessControlContext());
				}
				catch (PrivilegedActionException pae) {
					throw pae.getException();
				}
			}
			else {
				((InitializingBean) bean).afterPropertiesSet();
			}
		}

		if (mbd != null && bean.getClass() != NullBean.class) {
			String initMethodName = mbd.getInitMethodName();
			if (StringUtils.hasLength(initMethodName) &&
					!(isInitializingBean && "afterPropertiesSet".equals(initMethodName)) &&
					!mbd.isExternallyManagedInitMethod(initMethodName)) {
				invokeCustomInitMethod(beanName, bean, mbd);
			}
		}
	}



}

//抽象工厂有销毁bean的方法
public abstract class AbstractBeanFactory extends FactoryBeanRegistrySupport implements ConfigurableBeanFactory {
	@Override
	public void destroyBean(String beanName, Object beanInstance) {
		destroyBean(beanName, beanInstance, getMergedLocalBeanDefinition(beanName));
	}

	/**
	 * Destroy the given bean instance (usually a prototype instance
	 * obtained from this factory) according to the given bean definition.
	 * @param beanName the name of the bean definition
	 * @param bean the bean instance to destroy
	 * @param mbd the merged bean definition
	 */
	protected void destroyBean(String beanName, Object bean, RootBeanDefinition mbd) {
		//最终交给DisposableBeanAdapter 任意bean的适配器销毁处理
		new DisposableBeanAdapter(bean, beanName, mbd, getBeanPostProcessors(), getAccessControlContext()).destroy();
	}

}

org.springframework.beans.factory.support.DisposableBeanAdapter#destroy
	@Nullable
	private String inferDestroyMethodIfNecessary(Object bean, RootBeanDefinition beanDefinition) {
		String destroyMethodName = beanDefinition.getDestroyMethodName();
	
```