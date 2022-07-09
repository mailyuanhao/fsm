/**
 * @file 自动生成的框架文件，用户可以在该文件中实现action函数和guard函数
 *
 * @copyright Copyright (c) 2022
 *
 */
#include <memory>
#include <stdexcept>
#include "cd_machine.h"

namespace cd_machine
{
	void from_Closed_to_Opened_event_OpenClose_action(pMachine p, pBaseEvent)
	{
		throw std::logic_error("from_Closed_to_Opened_event_OpenClose_action not implemented");
	}

	void from_Opened_to_Closed_event_OpenClose_action(pMachine p, pBaseEvent)
	{
		throw std::logic_error("from_Opened_to_Closed_event_OpenClose_action not implemented");
	}

	void from_Closed_to_Playing_event_Play_action(pMachine p, pBaseEvent)
	{
		throw std::logic_error("from_Closed_to_Playing_event_Play_action not implemented");
	}

	// 0 for deny 1 for ok
	int from_Closed_to_Opened_event_OpenClose_guard(pMachine p, pBaseEvent)
	{
		throw std::logic_error("from_Closed_to_Opened_event_OpenClose_guard not implemented");
	}

	int from_Closed_to_Playing_event_Play_guard(pMachine p, pBaseEvent)
	{
		throw std::logic_error("from_Closed_to_Playing_event_Play_guard not implemented");
	}

	int from_Closed_to_PalyInvalid_event_Play_guard(pMachine p, pBaseEvent)
	{
		throw std::logic_error("from_Closed_to_PalyInvalid_event_Play_guard not implemented");
	}

	int from_Playing_to_Closed_event_Stop_guard(pMachine p, pBaseEvent)
	{
		throw std::logic_error("from_Playing_to_Closed_event_Stop_guard not implemented");
	}

	void unexpected_event_action(pMachine p, pBaseEvent e)
	{
		throw std::logic_error("unexpected_event_action not implemented");
	}

	class MachineWrapper;
	/**
	 * @brief 事件封装类
	 *
	 */
	class Event
	{
	public:
		friend class MachineWrapper;
		typedef std::shared_ptr<BaseEvent> EventPtr;
		explicit Event(int type, void *data)
		{
			auto p = new_event(type);
			if (!p)
			{
				throw std::runtime_error("event type invalid or not enough memory");
			}
			reset_user_data(data);
			e_.reset(p, delete_event);
		}

		// 请自行保障返回值的生命周期
		const void *get_user_data() const { return e_->user_data; }
		void *get_user_data() { return e_->user_data; }
		void *reset_user_data(void *data)
		{
			void *t = e_->user_data;
			e_->user_data = data;
			return t;
		}

	private:
		EventPtr e_;
	};

	/**
	 * @brief 状态机封装类，请注意自行保障多线程安全
	 *
	 */
	class MachineWrapper
	{
	public:
		typedef std::shared_ptr<Machine> MachinePtr;
		explicit MachineWrapper(void *data)
		{
			auto p = new_machine();
			if (!p)
			{
				throw std::runtime_error("not enough memory");
			}
			reset_user_data(data);
			m_.reset(p, delete_machine);
		}

		// 请自行保障返回值的生命周期
		const void *get_user_data() const { return m_->user_data; }
		void *get_user_data() { return m_->user_data; }
		void *reset_user_data(void *data)
		{
			void *t = m_->user_data;
			m_->user_data = data;
			return t;
		}

		void process_event(Event &event)
		{
			process(m_.get(), event.e_.get());
		}

	private:
		MachinePtr m_;
	};
}